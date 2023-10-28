package main

import (
	"context"
	"time"

	"github.com/redis/go-redis/v9"
)

var redis_host string = "localhost"
var redis_port string = "6379"
var redis_addr string = redis_host + ":" + redis_port
var redis_dump_client = redis.NewClient(&redis.Options{
	Addr:     redis_addr,
	Password: "",
	DB:       0,
})
var redis_dump_ctx = context.Background()
var redis_user_client = redis.NewClient(&redis.Options{
	Addr:     redis_addr,
	Password: "",
	DB:       1,
})
var redis_user_ctx = context.Background()
var redis_rdfs_client = redis.NewClient(&redis.Options{
	Addr:     redis_addr,
	Password: "",
	DB:       2,
})
var redis_rdfs_ctx = context.Background()

func _redis(args []string) string {
	if len(args) == 0 {
		return _redis_help()
	}
	s := args[1:]
	switch args[0] {
	case "list":
		return _redis_list(s)
	case "address":
		return redis_addr
	case "host":
		return redis_host
	case "port":
		return redis_port
	case "get":
		return _redis_get(s)
	case "set":
		return _redis_set(s)
	default:
		return _redis_error(args[0])
	}
}

var _redis_help = func() string {
	return "command <redis> help:\n"
}

var _redis_list = func(args []string) string {
	if len(args) > 0 {
		return _redis_error("invalid options, expected: redis list")
	}
	return "nothing to see here..."
}

var _redis_get = func(args []string) string {
	if len(args) != 2 {
		return _redis_error("invalid options, expected: redis get <db> <key>")
	}
	return redis_get(args[1], args[2])
}

var _redis_set = func(args []string) string {
	if len(args) != 3 {
		return _redis_error("invalid options, expected: redis set <db> <key> <value>")
	}
	redis_set(args[1], args[2], args[3])
	return "redis." + args[1] + "." + args[2] + "=" + args[3]
}

var _redis_error = func(msg string) string {
	return "command <redis> error: " + msg
}

func redis_set(db string, key string, value string) {
	switch db {
	case "dump":
		err := redis_dump_client.Set(redis_dump_ctx, key, value, 1*time.Minute).Err()
		logError("redis.set", err.Error())
	case "rdfs":
		err := redis_dump_client.Set(redis_user_ctx, key, value, 2*time.Minute).Err()
		logError("redis.set", err.Error())
	case "user":
		err := redis_dump_client.Set(redis_rdfs_ctx, key, value, 3*time.Minute).Err()
		logError("redis.set", err.Error())
	default:
		logError("redis.set", "invalid database option `"+db+"`")
	}
}

func redis_get(db string, key string) string {
	switch db {
	case "dump":
		return redis_dump_client.Get(redis_dump_ctx, key).Val()
	case "rdfs":
		return redis_rdfs_client.Get(redis_rdfs_ctx, key).Val()
	case "user":
		return redis_user_client.Get(redis_user_ctx, key).Val()
	default:
		return logError("redis.get", "invalid database option `"+db+"`")
	}
}

func redis_default(db string, key string, value string) string {
	var current string = redis_get(db, key)
	if current == "" && value != "" {
		logWarning("redis.default", "defaulted cache "+key+"="+value)
		redis_set(db, key, value)
		return value
	}
	return current
}
