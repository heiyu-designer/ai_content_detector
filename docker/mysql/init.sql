-- Unbot AI 数据库初始化脚本

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS unbot_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE unbot_ai;

-- 用户表已在应用代码中通过 SQLAlchemy 创建
-- 此文件用于初始化默认数据或索引
