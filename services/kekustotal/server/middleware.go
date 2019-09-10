package server

import (
	"database/sql"
	"encoding/json"
	"net/http"
)

func loginRequired(handlerFunc http.HandlerFunc, db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		s, err := r.Cookie("session")

		if err != nil {
			w.WriteHeader(http.StatusForbidden)
			j := map[string]interface{}{
				"ok": false,
				"error": "Authentication required",
			}
			ret, _ := json.Marshal(j)
			_, _ = w.Write(ret)
			return
		}

		row := db.QueryRow(`
			SELECT COUNT(*)
			FROM users
			WHERE id=?
		`, s.Value)

		var cnt int
		_ = row.Scan(&cnt)

		if cnt == 0 {
			w.WriteHeader(http.StatusForbidden)
			j := map[string]interface{}{
				"ok": false,
				"error": "Authentication required",
			}
			ret, _ := json.Marshal(j)
			_, _ = w.Write(ret)
			return
		}

		handlerFunc.ServeHTTP(w, r)
	}
}
