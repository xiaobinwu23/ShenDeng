using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace ShenDeng.Web.Areas.Admin
{
    public class AdminRouter : AreaRegistration // 注册区域
    {
        public override string AreaName   //区域名
        {
            get { return "Admin"; }
        }
        public override void RegisterArea(AreaRegistrationContext context)
        {
            context.MapRoute(  //路由映射
                "Admin_Router",   //映射规则名，可随意起，但不能重复
                "Admin/{controller}/{action}/{id}", //映射规则
                new {controller = "Admin", action = "Index", id = UrlParameter.Optional}, //默认值
                new[] {"ShenDeng.Web.Areas.Admin.Controllers"}  //命名空间，用于跨命名空间路由
                );
        }
    }
}