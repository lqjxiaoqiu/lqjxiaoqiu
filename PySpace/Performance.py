#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import math
import psutil
import platform
import multiprocessing
from datetime import datetime

# 确保中文正常显示
os.environ['LANG'] = 'zh_CN.UTF-8'

class PerformanceTester:
    """电脑性能测试工具"""
    
    def __init__(self):
        self.results = {}
        self.cpu_count = multiprocessing.cpu_count()
        self.mem_total = psutil.virtual_memory().total / (1024**3)  # GB
        
    def test_cpu_fibonacci(self, n=35):
        """斐波那契数列递归计算测试"""
        def fib(x):
            return x if x <= 1 else fib(x-1) + fib(x-2)
        
        start_time = time.time()
        result = fib(n)
        end_time = time.time()
        self.results['cpu_fibonacci'] = {
            'n': n,
            'result': result,
            'time': end_time - start_time
        }
        return self.results['cpu_fibonacci']
    
    def test_cpu_prime(self, n=1000000):
        """素数筛选测试 (埃拉托斯特尼筛法)"""
        start_time = time.time()
        
        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False
        for i in range(2, int(math.sqrt(n)) + 1):
            if sieve[i]:
                sieve[i*i : n+1 : i] = [False] * len(sieve[i*i : n+1 : i])
        
        prime_count = sum(sieve)
        end_time = time.time()
        self.results['cpu_prime'] = {
            'n': n,
            'prime_count': prime_count,
            'time': end_time - start_time
        }
        return self.results['cpu_prime']
    
    def test_cpu_matrix(self, size=2000):
        """矩阵乘法测试"""
        import numpy as np
        
        # 创建随机矩阵
        matrix_a = np.random.rand(size, size)
        matrix_b = np.random.rand(size, size)
        
        start_time = time.time()
        result = np.dot(matrix_a, matrix_b)
        end_time = time.time()
        
        self.results['cpu_matrix'] = {
            'matrix_size': f"{size}x{size}",
            'time': end_time - start_time
        }
        return self.results['cpu_matrix']
    
    def test_memory(self, size_mb=1024):
        """内存读写速度测试"""
        size_bytes = size_mb * 1024 * 1024
        data = bytearray(size_bytes)
        
        # 内存写入测试
        start_write = time.time()
        for i in range(size_bytes):
            data[i] = i % 256
        end_write = time.time()
        
        # 内存读取测试
        sum_val = 0
        start_read = time.time()
        for i in range(size_bytes):
            sum_val += data[i]
        end_read = time.time()
        
        write_speed = size_mb / (end_write - start_write)
        read_speed = size_mb / (end_read - start_read)
        
        self.results['memory'] = {
            'size_mb': size_mb,
            'write_speed_mb_per_sec': write_speed,
            'read_speed_mb_per_sec': read_speed,
            'checksum': sum_val
        }
        return self.results['memory']
    
    def test_disk(self, size_mb=1024, block_size_kb=4):
        """磁盘读写速度测试"""
        import tempfile
        
        block_size = block_size_kb * 1024
        blocks = (size_mb * 1024 * 1024) // block_size
        data = os.urandom(block_size)
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_file = f.name
            
            # 磁盘写入测试
            start_write = time.time()
            for _ in range(blocks):
                f.write(data)
            f.flush()
            os.fsync(f.fileno())
            end_write = time.time()
            
            # 重置文件指针
            f.seek(0)
            
            # 磁盘读取测试
            start_read = time.time()
            for _ in range(blocks):
                f.read(block_size)
            end_read = time.time()
        
        # 计算速度
        write_speed = size_mb / (end_write - start_write)
        read_speed = size_mb / (end_read - start_read)
        
        # 删除临时文件
        os.remove(temp_file)
        
        self.results['disk'] = {
            'size_mb': size_mb,
            'block_size_kb': block_size_kb,
            'write_speed_mb_per_sec': write_speed,
            'read_speed_mb_per_sec': read_speed
        }
        return self.results['disk']
    
    def get_system_info(self):
        """获取系统信息"""
        return {
            'os': platform.system() + " " + platform.version(),
            'hostname': platform.node(),
            'python_version': platform.python_version(),
            'cpu_model': platform.processor(),
            'cpu_count': self.cpu_count,
            'memory_total_gb': round(self.mem_total, 2),
            'test_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def generate_report(self):
        """生成测试报告"""
        system_info = self.get_system_info()
        
        report = "\n" + "="*50 + "\n"
        report += "系统信息\n" + "-"*50 + "\n"
        report += f"操作系统: {system_info['os']}\n"
        report += f"主机名: {system_info['hostname']}\n"
        report += f"Python版本: {system_info['python_version']}\n"
        report += f"CPU型号: {system_info['cpu_model']}\n"
        report += f"CPU核心数: {system_info['cpu_count']}\n"
        report += f"总内存: {system_info['memory_total_gb']} GB\n"
        report += f"测试时间: {system_info['test_time']}\n"
        report += "="*50 + "\n\n"
        
        # CPU测试结果
        if 'cpu_fibonacci' in self.results:
            fib = self.results['cpu_fibonacci']
            report += f"斐波那契数列计算 (n={fib['n']}): {fib['time']:.4f} 秒\n"
        
        if 'cpu_prime' in self.results:
            prime = self.results['cpu_prime']
            report += f"素数筛选 (n={prime['n']}): 找到 {prime['prime_count']} 个素数，耗时 {prime['time']:.4f} 秒\n"
        
        if 'cpu_matrix' in self.results:
            matrix = self.results['cpu_matrix']
            report += f"矩阵乘法 ({matrix['matrix_size']}): {matrix['time']:.4f} 秒\n"
        
        # 内存测试结果
        if 'memory' in self.results:
            mem = self.results['memory']
            report += f"\n内存测试 ({mem['size_mb']} MB):\n"
            report += f"  写入速度: {mem['write_speed_mb_per_sec']:.2f} MB/秒\n"
            report += f"  读取速度: {mem['read_speed_mb_per_sec']:.2f} MB/秒\n"
        
        # 磁盘测试结果
        if 'disk' in self.results:
            disk = self.results['disk']
            report += f"\n磁盘测试 ({disk['size_mb']} MB, 块大小 {disk['block_size_kb']} KB):\n"
            report += f"  写入速度: {disk['write_speed_mb_per_sec']:.2f} MB/秒\n"
            report += f"  读取速度: {disk['read_speed_mb_per_sec']:.2f} MB/秒\n"
        
        report += "\n" + "="*50 + "\n"
        return report
    
    def run_all_tests(self, disk_test=True):
        """运行所有测试"""
        print("开始性能测试，请稍候...")
        
        print("\nCPU 性能测试:")
        print("  正在计算斐波那契数列...", end=" ")
        self.test_cpu_fibonacci()
        print("完成")
        
        print("  正在筛选素数...", end=" ")
        self.test_cpu_prime()
        print("完成")
        
        print("  正在进行矩阵乘法...", end=" ")
        self.test_cpu_matrix()
        print("完成")
        
        print("\n内存性能测试:")
        print("  正在测试内存读写速度...", end=" ")
        self.test_memory()
        print("完成")
        
        if disk_test:
            print("\n磁盘性能测试:")
            print("  正在测试磁盘读写速度...", end=" ")
            self.test_disk()
            print("完成")
        
        report = self.generate_report()
        print(report)
        
        # 保存报告到文件
        with open("performance_report.txt", "w", encoding="utf-8") as f:
            f.write(report)
        print(f"完整报告已保存到: performance_report.txt")


if __name__ == "__main__":
    tester = PerformanceTester()
    
    # 检查是否安装了numpy
    try:
        import numpy
    except ImportError:
        print("警告: 未安装numpy库，矩阵乘法测试将被跳过")
        tester.test_cpu_matrix = lambda: None  # 禁用矩阵测试
    
    # 运行测试
    tester.run_all_tests()