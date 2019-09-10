package server

import (
	"bytes"
	"database/sql"
	"encoding/json"
	"fmt"
	"github.com/google/uuid"
	"github.com/sirupsen/logrus"
	"io"
	"io/ioutil"
	"kekustotal/patterns"
	"net/http"
	"os"
	"strconv"
	"strings"
)

func register(db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if r.Method == "POST" {
			username := r.FormValue("username")
			password := r.FormValue("password")

			row := db.QueryRow(`
				SELECT COUNT(*)
				FROM users
				WHERE username=?
			`, username)

			var cnt int
			err := row.Scan(&cnt)

			if err != nil {
				w.WriteHeader(http.StatusInternalServerError)
				logrus.Error("Error accessing database: ", err)
				return
			}

			if cnt > 0 {
				w.WriteHeader(http.StatusForbidden)
				j := map[string]interface{}{
					"ok": false,
					"error": "User already exists",
				}
				ret, _ := json.Marshal(j)
				_, _ = w.Write(ret)
				return
			}

			u := uuid.New()
			idx := u.String()

			_, err = db.Exec(`
				INSERT INTO users
				(
				 	id,
					username,
					password
				)
				VALUES
				(
					?, ?, ?
				)
			`, idx, username, password)

			if err != nil {
				w.WriteHeader(http.StatusInternalServerError)
				logrus.Error("Error accessing database: ", err)
				return
			}

			j := map[string]interface{}{
				"ok": true,
				"result": "OK",
			}
			ret, _ := json.Marshal(j)

			_, _ = w.Write(ret)
		}
	}
}

func login(db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if r.Method == "POST" {
			username := r.FormValue("username")
			password := r.FormValue("password")

			row := db.QueryRow(`
				SELECT id
				FROM users
				WHERE username=? and password=?
			`, username, password)

			var idx string

			err := row.Scan(&idx)

			if err == sql.ErrNoRows {
				w.WriteHeader(http.StatusForbidden)

				j := map[string]interface{}{
					"ok": false,
					"error": "No such user",
				}
				ret, _ := json.Marshal(j)
				_, _ = w.Write(ret)
				return
			}

			http.SetCookie(w, &http.Cookie{
				Name:  "session",
				Value: idx,
				Path:  "/",
			})

			j := map[string]interface{}{
				"ok": true,
				"error": "OK",
			}
			ret, _ := json.Marshal(j)

			_, _ = w.Write(ret)
		}
	}
}

func upload(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" {
		file, _, err := r.FormFile("file")

		if err != nil {
			w.WriteHeader(http.StatusForbidden)

			j := map[string]interface{}{
				"ok": false,
				"error": "No such field",
			}
			ret, _ := json.Marshal(j)
			_, _ = w.Write(ret)
			return
		}

		u := uuid.New()
		idx := u.String()

		f, _ := os.Create(fmt.Sprintf("resources/files/%s", idx))

		_, err = io.Copy(f, file)

		_ = f.Close()

		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			logrus.Error("Error creating file: ", err)
			return
		}

		_ = f.Close()

		s, _ := r.Cookie("session")

		f, _ = os.Create(fmt.Sprintf("resources/perms/%s-%s", s.Value, idx))

		_, _ = f.Write([]byte("access"))

		j := map[string]interface{}{
			"ok": true,
			"result": idx,
		}
		ret, _ := json.Marshal(j)

		_, _ = w.Write(ret)
	}
}

func invite(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" {
		fileIdx := r.FormValue("fileId")
		userIdx := r.FormValue("userId")
		s, _ := r.Cookie("session")
		ownerIdx := s.Value

		f, err := os.Open(fmt.Sprintf("resources/perms/%s-%s", ownerIdx, fileIdx))

		if err != nil {
			w.WriteHeader(http.StatusForbidden)

			j := map[string]interface{}{
				"ok": false,
				"error": "No access",
			}
			ret, _ := json.Marshal(j)
			_, _ = w.Write(ret)
			return
		}

		access, _ := ioutil.ReadAll(f)

		_ = f.Close()

		if !bytes.Equal(access, []byte("access")) {
			w.WriteHeader(http.StatusForbidden)

			j := map[string]interface{}{
				"ok": false,
				"error": "No access",
			}
			ret, _ := json.Marshal(j)
			_, _ = w.Write(ret)
			return
		}

		f, _ = os.Create(fmt.Sprintf("resources/perms/%s-%s", userIdx, fileIdx))

		_, _ = f.Write([]byte("access"))

		_ = f.Close()
	}
}

func forbid(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" {
		fileIdx := r.FormValue("fileId")
		userIdx := r.FormValue("userId")
		s, _ := r.Cookie("session")
		ownerIdx := s.Value

		f, err := os.Open(fmt.Sprintf("resources/perms/%s-%s", ownerIdx, fileIdx))

		if err != nil {
			w.WriteHeader(http.StatusForbidden)

			j := map[string]interface{}{
				"ok": false,
				"error": "No access",
			}
			ret, _ := json.Marshal(j)
			_, _ = w.Write(ret)
			return
		}

		access, _ := ioutil.ReadAll(f)

		_ = f.Close()

		if !bytes.Equal(access, []byte("access")) {
			w.WriteHeader(http.StatusForbidden)

			j := map[string]interface{}{
				"ok": false,
				"error": "No access",
			}
			ret, _ := json.Marshal(j)
			_, _ = w.Write(ret)
			return
		}

		f, _ = os.Create(fmt.Sprintf("resources/perms/%s-%s", userIdx, fileIdx))

		_, _ = f.Write([]byte("forbid"))

		_ = f.Close()
	}
}

func list(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		files, err := ioutil.ReadDir("resources/signs")

		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			logrus.Error("Error listing signs directory")
			return
		}

		var res []string

		for _, f := range files {
			if !f.IsDir() && !strings.HasPrefix(f.Name(), ".") {
				res = append(res, f.Name())
			}
		}

		j := map[string]interface{}{
			"ok": true,
			"result": res,
		}
		ret, _ := json.Marshal(j)

		_, _ = w.Write(ret)
	}
}

func download(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		fileIdx := r.FormValue("fileId")

		s, _ := r.Cookie("session")

		userIdx := s.Value

		f, err := os.Open(fmt.Sprintf("resources/perms/%s-%s", userIdx, fileIdx))

		if err != nil {
			w.WriteHeader(http.StatusForbidden)

			j := map[string]interface{}{
				"ok":    false,
				"error": "No access",
			}
			ret, _ := json.Marshal(j)
			_, _ = w.Write(ret)
			return
		}

		access, _ := ioutil.ReadAll(f)

		_ = f.Close()

		if !bytes.Equal(access, []byte("access")) {
			w.WriteHeader(http.StatusForbidden)

			j := map[string]interface{}{
				"ok": false,
				"error": "No access",
			}
			ret, _ := json.Marshal(j)
			_, _ = w.Write(ret)
			return
		}

		http.ServeFile(w, r, fmt.Sprintf("resources/files/%s", fileIdx))
	}
}

func info(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		fileIdx := r.FormValue("fileId")

		f, _ := os.Open(fmt.Sprintf("resources/stats/%s/virus", fileIdx))

		buf, _ := ioutil.ReadAll(f)
		virus, _ := strconv.Atoi(string(buf))

		_ = f.Close()

		f, _ = os.Open(fmt.Sprintf("resources/stats/%s/notvirus", fileIdx))

		buf, _ = ioutil.ReadAll(f)
		notVirus, _ := strconv.Atoi(string(buf))

		_ = f.Close()

		files, err := ioutil.ReadDir(fmt.Sprintf("resources/stats/%s/patterns", fileIdx))

		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			logrus.Error("Error listing stats directory")
			return
		}

		var res []string

		for _, f := range files {
			if !f.IsDir() && !strings.HasPrefix(f.Name(), ".") {
				res = append(res, f.Name())
			}
		}

		var reviews []map[string]string

		for _, p := range res {
			f, _ = os.Open(fmt.Sprintf("resources/signs/%s", p))
			buf, _ := ioutil.ReadAll(f)
			_ = f.Close()
			reviews = append(reviews, map[string]string{
				"sign": p,
				"res":  string(buf),
			})
		}

		j := map[string]interface{}{
			"virus": virus,
			"notVirus": notVirus,
			"reviews": reviews,
		}

		ret, _ := json.Marshal(j)

		_, _ = w.Write(ret)
	}
}

func signature(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" {
		fileIdx := r.FormValue("fileId")
		fileType := r.FormValue("fileType")

		if fileType == "malware" || fileType == "trojan" || fileType == "warm" {
			fileType = "virus"
		}

		s, _ := r.Cookie("session")

		f, err := os.Open(fmt.Sprintf("resources/perms/%s-%s", s.Value, fileIdx))

		if err == nil {
			access, _ := ioutil.ReadAll(f)

			_ = f.Close()

			if !bytes.Equal(access, []byte("access")) {
				w.WriteHeader(http.StatusForbidden)

				j := map[string]interface{}{
					"ok": false,
					"error": "No access",
				}
				ret, _ := json.Marshal(j)
				_, _ = w.Write(ret)
				return
			}

			_ = f.Close()
		}

		file, err := os.Open(fmt.Sprintf("resources/files/%s", fileIdx))

		if err != nil {
			w.WriteHeader(http.StatusBadRequest)

			j := map[string]interface{}{
				"ok": false,
				"error": "Invalid file",
			}
			ret, _ := json.Marshal(j)
			_, _ = w.Write(ret)
			return
		}

		offsetsForm := strings.Split(r.FormValue("offsets"), ",")

		offsets := make([]int64, 0, len(offsetsForm))

		for _, offset := range offsetsForm {
			o, err := strconv.Atoi(offset)
			offsets = append(offsets, int64(o))
			if err != nil {
				w.WriteHeader(http.StatusBadRequest)

				j := map[string]interface{}{
					"ok": false,
					"error": "Invalid offset",
				}
				ret, _ := json.Marshal(j)
				_, _ = w.Write(ret)
				return
			}
		}

		stat, _ := file.Stat()

		pattern, err := patterns.Calc(file, stat.Size(), offsets)

		_ = file.Close()

		if len(offsets) != 16 {
			w.WriteHeader(http.StatusBadRequest)

			j := map[string]interface{}{
				"ok": false,
				"error": "Invalid offsets",
			}
			ret, _ := json.Marshal(j)
			_, _ = w.Write(ret)
			return
		}

		if err != nil {
			w.WriteHeader(http.StatusBadRequest)

			j := map[string]interface{}{
				"ok": false,
				"error": fmt.Sprintf("Error calculating pattern: %s", err),
			}
			ret, _ := json.Marshal(j)
			_, _ = w.Write(ret)
			return
		}

		f, _ = os.Create(fmt.Sprintf("resources/signs/%s", pattern))

		_, _ = f.Write([]byte(fileType))

		_ = f.Close()

		_ = os.MkdirAll(fmt.Sprintf("resources/stats/%s/patterns", fileIdx), os.ModePerm)

		f, _ = os.Create(fmt.Sprintf("resources/stats/%s/patterns/%s", fileIdx, string(pattern)))

		_ = f.Close()

		f, _ = os.Open(fmt.Sprintf("resources/stats/%s/virus", fileIdx))

		buf, _ := ioutil.ReadAll(f)
		virus, _ := strconv.Atoi(string(buf))

		_ = f.Close()

		f, _ = os.Open(fmt.Sprintf("resources/stats/%s/notvirus", fileIdx))

		buf, _ = ioutil.ReadAll(f)
		notVirus, _ := strconv.Atoi(string(buf))

		_ = f.Close()

		if fileType == "virus" {
			virus += 1
		} else {
			notVirus += 1
		}

		f, _ = os.Create(fmt.Sprintf("resources/stats/%s/virus", fileIdx))

		_, _ = f.Write([]byte(strconv.Itoa(virus)))

		_ = f.Close()

		f, _ = os.Create(fmt.Sprintf("resources/stats/%s/notvirus", fileIdx))

		_, _ = f.Write([]byte(strconv.Itoa(notVirus)))

		_ = f.Close()

		j := map[string]interface{}{
			"ok": true,
			"result": map[string]string{
				"pattern": string(pattern),
			},
		}
		ret, _ := json.Marshal(j)

		_, _ = w.Write(ret)
	} else if r.Method == "GET" {
		fileIdx := r.FormValue("fileId")

		file, err := os.Open(fmt.Sprintf("resources/files/%s", fileIdx))

		if err != nil {
			w.WriteHeader(http.StatusBadRequest)

			j := map[string]interface{}{
				"ok": false,
				"error": "Invalid file",
			}
			ret, _ := json.Marshal(j)
			_, _ = w.Write(ret)
			return
		}

		offsetsForm := strings.Split(r.FormValue("offsets"), ",")

		offsets := make([]int64, 0, len(offsetsForm))

		for _, offset := range offsetsForm {
			o, err := strconv.Atoi(offset)
			offsets = append(offsets, int64(o))
			if err != nil {
				w.WriteHeader(http.StatusBadRequest)

				j := map[string]interface{}{
					"ok": false,
					"error": "Invalid offset",
				}
				ret, _ := json.Marshal(j)
				_, _ = w.Write(ret)
				return
			}
		}

		stat, _ := file.Stat()

		pattern, err := patterns.Calc(file, stat.Size(), offsets)

		_ = file.Close()

		if len(offsets) != 16 {
			w.WriteHeader(http.StatusBadRequest)

			j := map[string]interface{}{
				"ok": false,
				"error": "Invalid offsets",
			}
			ret, _ := json.Marshal(j)
			_, _ = w.Write(ret)
			return
		}

		if err != nil {
			w.WriteHeader(http.StatusBadRequest)

			j := map[string]interface{}{
				"ok": false,
				"error": fmt.Sprintf("Error calculating pattern: %s", err),
			}
			ret, _ := json.Marshal(j)
			_, _ = w.Write(ret)
			return
		}

		f, _ := os.Open(fmt.Sprintf("resources/signs/%s", pattern))

		fileType, _ := ioutil.ReadAll(f)

		_ = f.Close()

		j := map[string]interface{}{
			"ok": true,
			"error": map[string]string{
				"pattern": string(pattern),
				"fileType": string(fileType),
			},
		}
		ret, _ := json.Marshal(j)

		_, _ = w.Write(ret)
	}
}
