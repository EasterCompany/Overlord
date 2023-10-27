package main

import (
	"context"

	"github.com/redis/go-redis/v9"
)

// dump db
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

// user db
var __user_cache_client__ = redis.NewClient(&redis.Options{
	Addr:     "localhost:6379",
	Password: "",
	DB:       1,
})
var __user_cache_ctx__ = context.Background()

func user_cache_default(key string, value string) string {
	current := user_cache_get(key)
	print("user.cache.default." + key + " = (" + current + " -> " + value + ")")
	user_cache_set(key, value)
	return value
}

func user_cache_set(key string, value interface{}) {
	err := __user_cache_client__.Set(__user_cache_ctx__, key, value, 0).Err()
	handle_error(err)
}

func user_cache_get(key string) string {
	return __user_cache_client__.Get(__user_cache_ctx__, key).Val()
}

// rdfs db
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
