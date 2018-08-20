using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Web.Mvc;
using ShenDeng.Framework.Base;
using ShenDeng.Framework.Domain;
using ShenDeng.Framework.Tools;

namespace ShenDeng.Framework.Handle
{
    [AttributeUsage(AttributeTargets.Class)]
    public class FilterAuthority : FilterAttribute, IAuthorizationFilter
    {
        private int roles;
        private MySessionService sessionService;
        public FilterAuthority(params Role[] roles)
        {
            this.roles = 0;
            init(roles);
            this.sessionService = new MySessionService();
        }

        private void init(Role[] roles)
        {
            foreach (var i in roles)
            {
                this.roles = this.roles | (int)i;
            }
        }
        //判断是否有权限,(反射时会自动调用此方法)
        public void OnAuthorization(AuthorizationContext filterContext)
        {
            var account = sessionService.GetAccount();
            if (account == null)
            {
                //重定向,加参数传递
                filterContext.Result = new RedirectResult("~/Account/Login?ErrorMessage="+"请先登录"); 
                return;
            }
            if ((roles & account.Roles) == 0)
            {
                filterContext.Controller.ViewData[Keys.ErrorMessage] = "无法访问！";
                filterContext.Controller.ViewData[Keys.ErrorReason] = "没有权限！";
                filterContext.Result = new ViewResult
                {
                    ViewName = "Error",
                    ViewData = filterContext.Controller.ViewData
                    
                };
            }
        }
    }
}
