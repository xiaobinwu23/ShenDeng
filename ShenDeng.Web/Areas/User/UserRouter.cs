using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace ShenDeng.Web.Areas.User
{
    public class UserRouter : AreaRegistration //注册区域
    {
        public override string AreaName  //区域名
        {
            get { return "User"; }
        }

        public override void RegisterArea(AreaRegistrationContext context)
        {
            context.MapRoute(
                "User_Router",
                "User/{controller}/{action}/{id}",
                new {controller = "User", action ="Index", id = UrlParameter.Optional},
                new[] {"ShenDeng.Web.Areas.User.Controllers"}
                );
        }
    }
}