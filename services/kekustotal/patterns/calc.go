package patterns

import (
	"debug/elf"
	"errors"
	"io"
)

func Calc(file io.ReaderAt, fileSize int64, offsets []int64) ([]byte, error) {
	e, _ := elf.NewFile(file)
	s := e.Section(".text")
	buf := make([]byte, s.Size)
	_, _ = file.ReadAt(buf, int64(s.Offset))

	pattern := []byte("")

	for _, offset := range offsets {
		if offset < 0 || offset >= fileSize - int64(s.Offset) {
			return nil, errors.New("invalid offset")
		}

		pattern = append(pattern, buf[offset])
	}

	return pattern, nil
}
