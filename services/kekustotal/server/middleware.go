package server

import (
	"database/sql"
	"encoding/json"
	"net/http"
)

func loginRequired(handlerFunc http.HandlerFunc, db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		u := GetUser(r, db)

		if u == nil {
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

func withJsonResponse(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		next.ServeHTTP(w, r)
	}
}
