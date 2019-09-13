package server

import (
	"context"
	"github.com/sirupsen/logrus"
	"net/http"
	"time"
)

type HttpServer struct {
	h *http.Server
}

func NewServer(router *http.ServeMux) *HttpServer {
	return &HttpServer{
		h: &http.Server{
			Addr:         "0.0.0.0:8080",
			ReadTimeout:  time.Second * 15,
			WriteTimeout: time.Second * 15,
			Handler:      router,
		},
	}
}

func (srv *HttpServer) Serve() {
	if err := srv.h.ListenAndServe(); err != http.ErrServerClosed {
		logrus.Fatal("Error serving http server: ", err)
	}
}

func (srv *HttpServer) Close() {
	_ = srv.h.Shutdown(context.TODO())
}
