using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Web.Routing;
using ShenDeng.Framework;
using ShenDeng.Framework.App_Start;

namespace ShenDeng.Web
{
    public class MvcApplication : HttpApplication
    {
        protected void Application_Start()
        {
            UnityIoC.RegisterComponents();     //依赖注入
            AreaRegistration.RegisterAllAreas();    //注册区域路由
            RouteConfig.RegisterRoutes(RouteTable.Routes);    //注册全局路由
            Global_Start.CreateAccount();   //创建账户
        }
    }
}
