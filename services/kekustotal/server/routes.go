package server

import (
	"database/sql"
	"net/http"
)

func SetupRoutes(router *http.ServeMux, db *sql.DB) {
	router.HandleFunc("/register/", register(db))
	router.HandleFunc("/login/", login(db))
	router.HandleFunc("/signature/", loginRequired(signature, db))
	router.HandleFunc("/upload/", loginRequired(upload, db))
	router.HandleFunc("/invite/", loginRequired(invite, db))
	router.HandleFunc("/forbid/", loginRequired(forbid, db))
	router.HandleFunc("/list/", loginRequired(list, db))
	router.HandleFunc("/download/", loginRequired(download, db))
	router.HandleFunc("/info/", loginRequired(info, db))
}
