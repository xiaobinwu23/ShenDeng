using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Web.Mvc;
using ShenDeng.Framework.Application;
using ShenDeng.Framework.Application.Imp;
using ShenDeng.Framework.App_Start;
using Unity;
using Unity.Mvc5;

namespace ShenDeng.Framework
{
    public static class UnityIoC
    {
        private static IUnityContainer container { get; set; }

        public static void RegisterComponents()
        {
            //实例化容器
			container = new UnityContainer();
            //加载程序集
            var assembly = new List<string>();
            assembly.Add("ShenDeng.Framework");
           // assembly.Add("ShenDeng");
            //根据特性进行自动注册
            foreach (var ass in assembly)
            {
                RegisterType(ass);
            }

            DependencyResolver.SetResolver(new UnityDependencyResolver(container));  //?  他自己加的
        }

        public static void RegisterType(string assembly)
        {
            //得到所有类型
            var types = Assembly.Load(assembly).GetTypes();
            foreach (var type in types)
            {
                //得到所有自定义特性
                var attributes = type.GetCustomAttributes();
                foreach (var attribute in attributes)
                {
                    if (attribute is RegisterToContainerAttribute)
                    {
                        //得到所有接口
                        var Itypes = type.GetInterfaces();
                        //获得唯一接口，如果不是唯一的就会报错
                        var Itype = Itypes.Single();
                        //注册类型
                        container.RegisterType(Itype, type);
                    }
                }
            }
        }
        //直接通过接口类型获取实例
        public static T  Get<T>()
        {
            try
            {
                return container.Resolve<T>();
            }
            catch (Exception e)
            {
                throw new Exception(typeof(T)+"注册有误!\n"+e.Message);
            }
            
        }
    }
}