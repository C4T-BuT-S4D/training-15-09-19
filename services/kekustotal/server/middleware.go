package server

import (
	"compress/gzip"
	"database/sql"
	"encoding/json"
	"io"
	"net/http"
	"strings"
)

func loginRequired(handlerFunc http.HandlerFunc, db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		u := GetUser(r, db)

		if u == nil {
			w.WriteHeader(http.StatusForbidden)
			j := map[string]interface{}{
				"ok":    false,
				"error": "Authentication required",
			}
			ret, _ := json.Marshal(j)
			_, _ = w.Write(ret)
			return
		}

		handlerFunc.ServeHTTP(w, r)
	}
}

type gzipResponseWriter struct {
	io.Writer
	http.ResponseWriter
}

func (w gzipResponseWriter) Write(b []byte) (int, error) {
	return w.Writer.Write(b)
}

func withGzipCompression(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if strings.Contains(r.Header.Get("Accept-Encoding"), "gzip") {
			w.Header().Set("Content-Encoding", "gzip")
			gz := gzip.NewWriter(w)
			defer gz.Close()
			gzw := gzipResponseWriter{gz, w}
			next.ServeHTTP(gzw, r)
		} else {
			next.ServeHTTP(w, r)
		}
	}
}

func withJsonResponse(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		next.ServeHTTP(w, r)
	}
}
