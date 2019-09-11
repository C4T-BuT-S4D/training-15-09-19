package server

import (
	"database/sql"
	"fmt"
	"github.com/sirupsen/logrus"
	"html/template"
	"net/http"
)

type User struct {
	Idx   string
	Login string
}

func GetUser(r *http.Request, db *sql.DB) *User {
	s, err := r.Cookie("session")

	if err != nil {
		return nil
	}

	row := db.QueryRow(`
		SELECT id, username
		FROM users
		WHERE id=?
	`, s.Value)

	var u User
	err = row.Scan(&u.Idx, &u.Login)

	if err != nil {
		return nil
	}

	return &u
}

func renderWithContext(w http.ResponseWriter, templ string, ctx interface{}) {
	mainTemplate := template.New("base")
	mainTemplate, err := mainTemplate.ParseFiles("templates/base.html")
	if err != nil {
		logrus.Error(err)
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	t := template.Must(mainTemplate.ParseFiles(fmt.Sprintf("templates/%s", templ)))
	err = t.Execute(w, ctx)

	if err != nil {
		logrus.Error(err)
		w.WriteHeader(http.StatusInternalServerError)
	}
}
