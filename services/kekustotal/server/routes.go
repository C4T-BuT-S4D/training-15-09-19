package server

import (
	"database/sql"
	"net/http"
)

func SetupRoutes(router *http.ServeMux, db *sql.DB) {
	router.HandleFunc("/api/register/", withJsonResponse(register(db)))
	router.HandleFunc("/api/login/", withJsonResponse(login(db)))
	router.HandleFunc("/api/logout/", withJsonResponse(logout))
	router.HandleFunc("/api/signature/", withJsonResponse(loginRequired(signature, db)))
	router.HandleFunc("/api/upload/", withJsonResponse(loginRequired(upload, db)))
	router.HandleFunc("/api/invite/", withJsonResponse(loginRequired(invite, db)))
	router.HandleFunc("/api/forbid/", withJsonResponse(loginRequired(forbid, db)))
	router.HandleFunc("/api/list/", withJsonResponse(loginRequired(list, db)))
	router.HandleFunc("/api/info/", withJsonResponse(loginRequired(info, db)))

	router.HandleFunc("/download/", withJsonResponse(loginRequired(download, db)))

	fs := http.FileServer(http.Dir("public"))

	router.Handle("/public/", http.StripPrefix("/public/", fs))
	router.HandleFunc("/favicon.ico", func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "public/favicon.ico")
	})

	router.HandleFunc("/", pIndex(db))
	router.HandleFunc("/login/", pLogin(db))
	router.HandleFunc("/register/", pRegister(db))
	router.HandleFunc("/upload/", pUpload(db))
	router.HandleFunc("/info/", pInfo(db))
}
