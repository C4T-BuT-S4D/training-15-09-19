package main

import (
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
	"github.com/sirupsen/logrus"
	"kekustotal/server"
	"net/http"
	"os"
	"os/signal"
)

func main() {
	db, err := sql.Open("sqlite3", "file:resources/db.db")

	if err != nil {
		logrus.Fatal("Error opening database: ", err)
	}

	err = db.Ping()

	if err != nil {
		logrus.Fatal("Error connecting to database: ", err)
	}

	_, err = db.Exec(`
		CREATE TABLE IF NOT EXISTS users
		(
		    id       VARCHAR(50),
		    username VARCHAR(100),
			password VARCHAR(100)
		)
	`)

	if err != nil {
		logrus.Fatal("Error initialising users table: ", err)
	}

	router := http.NewServeMux()
	server.SetupRoutes(router, db)
	srv := server.NewServer(router)
	go srv.Serve()

	logrus.Info("Listening on port 8080")

	c := make(chan os.Signal, 1)

	signal.Notify(c, os.Interrupt)
	signal.Notify(c, os.Kill)

	<-c

	logrus.Info("Stopping http server")

	srv.Close()

	logrus.Info("Http server shutdown successful")
}
