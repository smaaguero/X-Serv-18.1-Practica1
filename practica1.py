#!/usr/bin/python3

import webapp
import urllib.parse
import csv



def preparecontent(content):
    if (content[0:7] != "http://" and
        content[0:8] != "https://"):
        content = "http://" + content
    return content


class acortadorUrl(webapp.webApp):

    content = {'/': 'Root page'}
    mirror = {'Root page': '/'}                 #Variables de clase
    index = 0;

    def inicializa(self):
        import os.path
        if os.path.isfile('basededatos.csv'):
            with open('basededatos.csv', 'r') as database:
                read = csv.reader(database, delimiter=',')
                self.index = 0
                for line in read:
                    self.content[line[0]] = line[1]
                    self.mirror[line[1]] = line[0]
                    self.index = self.index + 1

    def persiste(self):
        with open('basededatos.csv', 'w', newline='') as database:
            writer = csv.writer(database, delimiter=',')
            for element in self.content:
                writer.writerow([element, self.content[element]])


    def parse(self, request):
        """Return the resource name (including /)"""
        self.inicializa()
        return (request.split(' ', 1)[0], request.split(' ', 2)[1], request.split('=')[-1])


    def process(self, parsed):
        """Process the relevant elements of the request.
        Finds the HTML text corresponding to the resource name,
        ignoring requests for resources not in the dictionary.
        """
        method, resourceName, content = parsed

#Trazas
        print(method)
        print(resourceName)
        if method == "GET":
            print(content)
        elif method == "POST":
            print(urllib.parse.unquote(content))
        for key, value in self.content.items():
            print("###" + str(key) + "--->" + str(value))

        if method == "GET":
            if resourceName == "favicon.ico":
                httpCode = "404 Not Found"
                htmlBody = "<html><body><h1>Not Found</h1></body></html>"
            elif resourceName == "/":
                httpCode = "200 OK"
                htmlBody = "<html><body><br><p align='center'>Introduzca la url</p>" \
                      "<form method='POST'><p align='center'><input type='text' name='URL'><br></form>" \
                      "</body></html>"
            elif resourceName in self.content.keys():
                httpCode = "300 Redirect"
                htmlBody = "<html><body><meta http-equiv='refresh' content=0;url=" \
                                + self.content[resourceName] + ">" + "</p>" + "</body></html>"
            else:
                httpCode = "404 Not Found"
                htmlBody = "<html><body>Recurso no encontrado</body></html>"
        elif method == "POST":
            content = urllib.parse.unquote(content)
            if content == "":
                httpCode = "200 OK"
                htmlBody = "<html><body>Intenta meterme una URL porfa :)</body></html>"
            else:
                if content in self.mirror.keys():
                    httpCode = "200 OK"
                    recurso = self.mirror[content]
                    htmlBody = "<html><body>Recurso = " + recurso \
                                + "</body></html>"
                else:
                    content = preparecontent(content)
                    recurso = "/" + str(self.index + 1)
                    self.index += 1;
                    self.content[recurso] = content
                    self.mirror[content] = recurso
                    self.persiste()
                    recurso_2 = "http://localhost:1234" + recurso
                    httpCode = "200 OK"
                    htmlBody = "<html><body>Url a acortar = <a href=" +  self.content[recurso] \
                    + ">" + self.content[recurso] +"</a>" + "<br>Url Acortada = <a href="+ recurso_2 + ">" + recurso_2 + "</a>" \
                                + "</br></body></html>"
        else:
            httpCode = "404 Not Found"
            htmlBody = "<html><body>Metodo no conocido</body></html>"

        return (httpCode, htmlBody)

if __name__ == "__main__":
    testWebApp = acortadorUrl("localhost", 1234)
