package main

import (
	"bytes"
	"database/sql"
	"encoding/gob"
	"fmt"
	"log"
	"runtime"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

// ChannelData 对应新库 channel_data 字段的结构
// 只处理 EHZ, EHE, EHN 三个通道
// DataType 固定为 "int32"，ByteSize 固定为 4
// ChannelId: EHZ=1, EHE=2, EHN=3
// ChannelCode: 对应编码字符串
// Data 保存 int32 数组
// 新表 record_time 字段为毫秒级时间戳

type ChannelData struct {
	ChannelCode string  // 通道编码 EHZ/EHE/EHN
	ChannelId   int     // 通道 ID (1/2/3)
	ByteSize    int     // 字节大小，固定 4
	DataType    string  // 数据类型，固定 "int32"
	Data        []int32 // 通道数据
}

// Row 代表从旧表读取的一条记录
type Row struct {
	PK         int64
	CreatedAt  int64
	TSMillis   int64
	ZText      string
	EText      string
	NText      string
	SampleRate int
}

func main() {
	// 并发工作数量
	workers := runtime.NumCPU()

	// 打开旧数据库 sqlite.db
	oldDB, err := sql.Open("sqlite3", "sqlite.db")
	if err != nil {
		log.Fatalf("打开旧数据库失败: %v", err)
	}
	defer oldDB.Close()

	// 打开新数据库 sqlite_v4.db
	newDB, err := sql.Open("sqlite3", "sqlite_v4.db")
	if err != nil {
		log.Fatalf("打开新数据库失败: %v", err)
	}
	defer newDB.Close()

	// 启用 WAL 模式以支持并发写入
	if _, err := newDB.Exec("PRAGMA journal_mode=WAL"); err != nil {
		log.Printf("设置 WAL 模式失败: %v", err)
	}
	newDB.SetMaxOpenConns(workers)

	// 获取记录总数，用于进度
	var total int64
	if err := oldDB.QueryRow("SELECT COUNT(*) FROM adc_count").Scan(&total); err != nil {
		log.Fatalf("获取记录总数失败: %v", err)
	}
	log.Printf("总记录数: %d, 并发工作数: %d", total, workers)

	// 创建任务通道
	jobs := make(chan Row, workers*2)
	var wg sync.WaitGroup
	var processed uint64

	// 进度报告
	done := make(chan struct{})
	go func() {
		ticker := time.NewTicker(5 * time.Second)
		defer ticker.Stop()
		for {
			select {
			case <-done:
				return
			case <-ticker.C:
				p := atomic.LoadUint64(&processed)
				pct := float64(p) / float64(total) * 100
				log.Printf("Progress: %d/%d (%.2f%%)", p, total, pct)
			}
		}
	}()

	// 启动 worker
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for job := range jobs {
				// 转换文本为 int32 切片
				zData := parseTextToInt32Slice(job.ZText)
				eData := parseTextToInt32Slice(job.EText)
				nData := parseTextToInt32Slice(job.NText)

				// 构建 ChannelData 列表并 gob 编码
				cds := []ChannelData{
					{ChannelCode: "EHZ", ChannelId: 1, ByteSize: 4, DataType: "int32", Data: zData},
					{ChannelCode: "EHE", ChannelId: 2, ByteSize: 4, DataType: "int32", Data: eData},
					{ChannelCode: "EHN", ChannelId: 3, ByteSize: 4, DataType: "int32", Data: nData},
				}
				var buf bytes.Buffer
				enc := gob.NewEncoder(&buf)
				if err := enc.Encode(cds); err != nil {
					log.Printf("编码 gob 失败 (pk=%d): %v", job.PK, err)
					continue
				}
				channelBlob := buf.Bytes()

				// 计算表名
				tsSec := job.TSMillis / 1000
				nsec := (job.TSMillis % 1000) * int64(time.Millisecond)
				t := time.Unix(tsSec, nsec).UTC()
				dayOfYear := t.YearDay()
				tableIndex := dayOfYear % 366
				tableName := fmt.Sprintf("as_seis_records_%d", tableIndex)

				// 插入新库
				stmt := fmt.Sprintf(
					"INSERT OR IGNORE INTO %s (id, created_at, record_time, sample_rate, channel_data) VALUES (?, ?, ?, ?, ?)",
					tableName,
				)
				if _, err := newDB.Exec(stmt, job.PK, job.CreatedAt, job.TSMillis, job.SampleRate, channelBlob); err != nil {
					log.Printf("插入失败 (表=%s, pk=%d): %v", tableName, job.PK, err)
				}

				atomic.AddUint64(&processed, 1)
			}
		}()
	}

	// 读取旧库并分发任务
	rows, err := oldDB.Query("SELECT primary_key, created_at, timestamp, z_axis, e_axis, n_axis, sample_rate FROM adc_count")
	if err != nil {
		log.Fatalf("查询旧库记录失败: %v", err)
	}
	for rows.Next() {
		var r Row
		if err := rows.Scan(&r.PK, &r.CreatedAt, &r.TSMillis, &r.ZText, &r.EText, &r.NText, &r.SampleRate); err != nil {
			log.Printf("扫描记录失败: %v", err)
			continue
		}
		jobs <- r
	}
	rows.Close()

	// 所有任务已发送，关闭通道并等待完成
	close(jobs)
	wg.Wait()
	close(done)

	log.Println("迁移完成，处理记录数:", processed)
}

// parseTextToInt32Slice 将逗号分隔的字符串转换为 []int32
func parseTextToInt32Slice(s string) []int32 {
	s = strings.TrimSpace(s)
	if s == "" {
		return nil
	}
	parts := strings.Split(s, "|")
	data := make([]int32, 0, len(parts))
	for _, p := range parts {
		p = strings.TrimSpace(p)
		if p == "" {
			continue
		}
		v, err := strconv.ParseInt(p, 10, 32)
		if err != nil {
			log.Printf("警告: 解析整数失败 '%s': %v", p, err)
			continue
		}
		data = append(data, int32(v))
	}
	return data
}
