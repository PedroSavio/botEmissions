import pymysql


class DBFacade:

    def conectar(self, autocommit=False):
        return pymysql.connect(host='68.183.18.153', user='aluno', passwd='webglauco', db='project_web',
                               autocommit=autocommit)

    def atualizarNumeros(self, objeto):
        conexao = self.conectar(autocommit=True)
        cursor = conexao.cursor()
        for x in objeto:
            sql = f'''update co2 set total = {x.total}, coal = {x.coal}, gas = {x.gas}, oil = {x.oil}, cement = {x.cement}, flaring = {x.flaring}, other = {x.other}, per_capita = {x.per_capita} where country = {x.country} and year = {x.year}'''
            cursor.execute(sql)
            print(f'sql = ', sql)
        cursor.close()
        conexao.close()

    def quantidadeRegistro(self):
        conexao = self.conectar(autocommit=True)
        cursor = conexao.cursor()
        sql = f'''select count(*) from co2'''
        cursor.execute(sql)
        cursor.close()
        conexao.close()
        return cursor.fetchone()[0]
