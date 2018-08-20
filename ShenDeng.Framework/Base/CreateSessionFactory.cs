using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using FluentNHibernate.Cfg;
using FluentNHibernate.Cfg.Db;
using NHibernate;
using NHibernate.Cfg;
using NHibernate.Context;
using NHibernate.Tool.hbm2ddl;

namespace ShenDeng.Framework.Base
{
    public class CreateSessionFactory
    {
        //创建的数据库文件url
        private const string DbFile = "E:/dbFile/ShenDengHH.db";

        private static ISessionFactory sessionFactory;
        private static ISession session;
        public static ISessionFactory GetSessionFactory()
        {
            if (sessionFactory == null)   //单例模式
                sessionFactory = Fluently.Configure()   //读取核心配置文件
                    .Database(SQLiteConfiguration.Standard   //声明使用的数据库
                        .UsingFile(DbFile))   //使用文件数据库
                    .Mappings(m=>   //数据库映射，参数：映射文件所在的程序集
                          m.FluentMappings.AddFromAssembly(Assembly.Load("ShenDeng.Framework")))
                    .ExposeConfiguration(BuildSchema)   //导入数据库文件的模板
                    .BuildSessionFactory();   //配置完参数后开始创建 会话工厂

            return sessionFactory;
        }

        public static ISession GetSession()
        {
            if (session == null)   //单例
            {
                    session = GetSessionFactory().OpenSession();
                    session.BeginTransaction();
                    //CurrentSessionContext.Bind(session);//把session添加到线程中，以后通过GetCurrentSession()来获取。？*？还存在问题！报错：未找到UnityContainer.cs
                return session;
            }
            else
            {
                session.BeginTransaction();   //每次transaction.Commit()后，session会关闭；所以要重新BeginTransaction()来打开session
                return session;
            }

        }
        public static void BuildSchema(Configuration config)
        {
            var ex = File.Exists(DbFile) ? false : true; //当该文件存在时，不需要删除；
                                       //不存在时，则根据配置文件中的持久化类和映射关系创建数据库表。

            new SchemaExport(config)   //根据模板创建数据库
                .Execute(true, ex, false);   
        }
    }
}
