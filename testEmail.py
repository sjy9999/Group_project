# # # 这是一个  basic email   test   最后可删
# # # # # import yagmail

# # # # # try:
# # # # #     yag = yagmail.SMTP(user='s395615470@sina.com', password='s123456', host='smtp.sina.com', port=465, smtp_ssl=True)
# # # # #     yag.send(to='395615470@qq.com', subject='Test', contents='This is a test mail.')
# # # # #     print("Mail sent successfully!")
# # # # # except Exception as e:
# # # # #     print("Failed to send mail:", e)
# # # # import ssl
# # # # print(ssl.OPENSSL_VERSION)
# # # # print(ssl.PROTOCOL_TLS_CLIENT)

# # # import smtplib
# # # import ssl

# # # context = ssl.create_default_context()
# # # context.set_ciphers('DEFAULT@SECLEVEL=1')  # 降低安全级别

# # # try:
# # #     smtp_server = smtplib.SMTP('smtp.sina.com', 587)
# # #     smtp_server.starttls(context=context)  # 使用自定义的SSL上下文
# # #     smtp_server.login('s395615470@sina.com', 's123456')
# # #     smtp_server.sendmail('s395615470@sina.com', '395615470@qq.com', 'Subject: Test\n\nThis is a test mail.')
# # #     smtp_server.quit()
# # #     print("Mail sent successfully!")
# # # except Exception as e:
# # #     print("Failed to send mail:", e)


# # import smtplib
# # from email.mime.text import MIMEText
# # from email.mime.multipart import MIMEMultipart
# # from email.header import Header

# # # 创建 MIME 多部分消息对象
# # msg = MIMEMultipart()
# # msg['From'] = Header("24382608@student.uwa.edu.au")
# # msg['To'] = Header("recipient@example.com")
# # msg['Subject'] = Header('测试邮件')

# # # 邮件正文内容
# # body = "这是一个测试邮件，来自 Python 脚本。"
# # msg.attach(MIMEText(body, 'plain', 'utf-8'))

# # # SMTP 服务器连接设置
# # server = smtplib.SMTP('smtp.office365.com', 587)
# # server.starttls()  # 启用安全传输模式
# # try:
# #     server.login('24382608@student.uwa.edu.au', 'sjy.199346')
# #     server.sendmail('24382608@student.uwa.edu.au', ['recipient@example.com'], msg.as_string())
# #     print("邮件发送成功！")
# # except Exception as e:
# #     print("发送邮件失败:", e)
# # finally:
# #     server.quit()




# import smtplib

# try:
#     smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
#     smtp_server.starttls()
#     smtp_server.login('s395615470@gmail.com', 'johgpueksgsakecj')
#     smtp_server.sendmail('s395615470@gmail.com', '395615470@qq.com', 'Subject: Test\n\nThis is a test mail.')
#     smtp_server.quit()
#     print("Mail sent successfully!")
# except Exception as e:
#     print("Failed to send mail:", e)
