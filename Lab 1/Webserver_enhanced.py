#!/usr/bin/env python3
from datetime import datetime, timezone
from socket import *
import sys
import os
import select

def create_http_header(status_code, content_length=None, content_type="text/html"):
    """生成 HTTP 响应头"""
    now_utc = datetime.now(timezone.utc)
    http_date = now_utc.strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    header = (
        f"HTTP/1.1 {status_code}\r\n"
        f"Date: {http_date}\r\n"
        "Server: Linux-sssakana@sssakana-A320M-S2H\r\n"
    )
    
    if content_length is not None:
        header += f"Content-Length: {content_length}\r\n"
    
    header += f"Content-Type: {content_type}\r\n\r\n"
    return header

def send_file(connection_socket, filename):
    """发送文件内容"""
    try:
        with open(filename, 'rb') as f:
            content = f.read()
        
        _, ext = os.path.splitext(filename)
        content_types = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.jpg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.ico': 'image/x-icon',
            '.svg': 'image/svg+xml',
            '.json': 'application/json',
            '.pdf': 'application/pdf'
        }
        content_type = content_types.get(ext.lower(), 'application/octet-stream')
        
        header = create_http_header("200 OK", len(content), content_type)
        connection_socket.sendall(header.encode())
        connection_socket.sendall(content)
        
    except IOError:
        error_content = b"<h1>404 Not Found</h1>"
        header = create_http_header("404 Not Found", len(error_content))
        connection_socket.sendall(header.encode())
        connection_socket.sendall(error_content)
    except Exception as e:
        print(f"Error sending file: {e}")
        raise

def receive_full_request(connection_socket, timeout=5):
    """完整接收HTTP请求"""
    data = b''
    connection_socket.settimeout(timeout)
    
    try:
        while True:
            chunk = connection_socket.recv(4096)
            if not chunk:
                break
            data += chunk
            if b'\r\n\r\n' in data:  # 头部结束标志
                # 检查是否有Content-Length
                headers = data.split(b'\r\n\r\n')[0].decode('utf-8', errors='ignore')
                if 'Content-Length:' in headers:
                    content_length = int(headers.split('Content-Length:')[1].split('\r\n')[0].strip())
                    body_start = data.find(b'\r\n\r\n') + 4
                    while len(data) < body_start + content_length:
                        chunk = connection_socket.recv(4096)
                        if not chunk:
                            break
                        data += chunk
                break
    except timeout:
        print("Request receive timeout")
    except Exception as e:
        print(f"Error receiving request: {e}")
    
    return data.decode('utf-8', errors='ignore')

def handle_request(connection_socket):
    """处理客户端请求"""
    try:
        message = receive_full_request(connection_socket)
        if not message:
            return
        
        print(f"Received request:\n{message[:500]}...")  # 只打印前500字符
        
        # 解析请求行
        try:
            request_line = message.split('\r\n')[0]
            method, path, _ = request_line.split()
        except (IndexError, ValueError):
            error_content = b"<h1>400 Bad Request</h1>"
            header = create_http_header("400 Bad Request", len(error_content))
            connection_socket.sendall(header.encode())
            connection_socket.sendall(error_content)
            return
        
        if method != 'GET':
            error_content = b"<h1>405 Method Not Allowed</h1>"
            header = create_http_header("405 Method Not Allowed", len(error_content))
            connection_socket.sendall(header.encode())
            connection_socket.sendall(error_content)
            return
        
        if path == '/':
            path = '/index.html'
        
        filename = path.split('?')[0].split('#')[0][1:]  # 去掉查询参数和锚点
        
        # 安全限制
        if not filename or '..' in filename or filename.startswith('/'):
            error_content = b"<h1>403 Forbidden</h1>"
            header = create_http_header("403 Forbidden", len(error_content))
            connection_socket.sendall(header.encode())
            connection_socket.sendall(error_content)
            return
        
        send_file(connection_socket, filename)
        
    except ConnectionResetError:
        print("Client disconnected unexpectedly")
    except Exception as e:
        print(f"Error handling request: {e}")
        error_content = b"<h1>500 Internal Server Error</h1>"
        header = create_http_header("500 Internal Server Error", len(error_content))
        try:
            connection_socket.sendall(header.encode())
            connection_socket.sendall(error_content)
        except:
            pass
    finally:
        try:
            connection_socket.shutdown(SHUT_RDWR)
        except:
            pass
        connection_socket.close()

def main():
    server_port = 55555
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    
    try:
        server_socket.bind(('', server_port))
        server_socket.listen(5)
        server_socket.settimeout(1)  # 设置accept超时，便于响应Ctrl+C
        print(f"Server started on port {server_port}")
        
        while True:
            try:
                print('Ready to serve...')
                connection_socket, addr = server_socket.accept()
                print(f"Connection from {addr}")
                handle_request(connection_socket)
            except timeout:
                continue  # 超时后继续循环，检查是否有Ctrl+C
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(f"Error accepting connection: {e}")
                continue
                
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()
        sys.exit()

if __name__ == "__main__":
    main()
