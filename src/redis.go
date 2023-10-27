package main

import (
	"context"
	"time"

	"github.com/redis/go-redis/v9"
)

func _redis(args []string) string {
	if len(args) > 0 {
		switch args[0] {
		case "help":
			return _redis_help()
		case "list":
			return _redis_list()
		}
	}
	return _redis_error("invalid options")
}

var _redis_help = func() string {
	return "command <redis> help:\n"
}

var _redis_list = func() string {
	return "nothing to see here..."
}

var _redis_error = func(msg string) string {
	return "command <redis> error: " + msg
}

var __dump_cache_client__ = redis.NewClient(&redis.Options{
	Addr:     "localhost:6379",
	Password: "",
	DB:       0,
})
var __dump_cache_ctx__ = context.Background()

func dump(key string, value interface{}) {
	err := __dump_cache_client__.Set(__dump_cache_ctx__, key, value, 0).Err()
	handle_error(err)
}

func recycle(key string) {
	err := __dump_cache_client__.Get(__dump_cache_ctx__, key).Err()
	handle_error(err)
}

var __user_cache_client__ = redis.NewClient(&redis.Options{
	Addr:     "localhost:6379",
	Password: "",
	DB:       1,
})
var __user_cache_ctx__ = context.Background()

func user_cache_default(key string, value string) string {
	var current string = user_cache_get(key)
	if current == "" && value != "" {
		warn("defaulting user_cache >> " + key + ": " + value)
		user_cache_set(key, value)
		return value
	}
	return current
}

func user_cache_set(key string, value string) {
	err := __user_cache_client__.Set(__user_cache_ctx__, key, value, 10*time.Minute).Err()
	handle_error(err)
}

func user_cache_get(key string) string {
	return __user_cache_client__.Get(__user_cache_ctx__, key).Val()
}

var __rdfs_cache_client__ = redis.NewClient(&redis.Options{
	Addr:     "localhost:6379",
	Password: "",
	DB:       2,
})
var __rdfs_cache_ctx__ = context.Background()

func rdfs_cache_set(key string, value interface{}) {
	err := __rdfs_cache_client__.Set(__rdfs_cache_ctx__, key, value, 0).Err()
	handle_error(err)
}

func rdfs_cache_get(key string) {
	err := __rdfs_cache_client__.Get(__rdfs_cache_ctx__, key).Err()
	handle_error(err)
}
