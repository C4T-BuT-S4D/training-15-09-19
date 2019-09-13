package patterns

import (
	"debug/elf"
	"encoding/hex"
	"errors"
	"io"
)

func convert(b byte) []byte {
	if 32 <= b && b < 127 {
		return []byte{b}
	}
	buf := hex.EncodeToString([]byte{b})
	buf = "\\x" + buf
	return []byte(buf)
}

func Calc(file io.ReaderAt, fileSize int64, offsets []int64) ([]byte, error) {
	e, _ := elf.NewFile(file)
	s := e.Section(".text")
	buf := make([]byte, fileSize-int64(s.Offset))
	_, _ = file.ReadAt(buf, int64(s.Offset))

	pattern := []byte("")

	for _, offset := range offsets {
		if offset < 0 || offset >= fileSize-int64(s.Offset) {
			return nil, errors.New("invalid offset")
		}

		app := convert(buf[offset])

		for _, c := range app {
			pattern = append(pattern, c)
		}
	}

	return pattern, nil
}
