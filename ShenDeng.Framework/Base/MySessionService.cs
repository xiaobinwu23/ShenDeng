using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Web.Security;
using ShenDeng.Framework.Domain;
using System.Web;
using ShenDeng.Framework.App_Start;
using ShenDeng.Framework.Tools;

namespace ShenDeng.Framework.Base
{
    [RegisterToContainer]
    public class MySessionService : IMySessionService
    {
        public void Login(string username, bool rememberMe)
        {
            FormsAuthentication.SetAuthCookie(username, rememberMe);
        }

        public void SignOut()
        {
            FormsAuthentication.SignOut();
        }

        public void SaveAccount(Account account)
        {
            HttpContext.Current.Session.Add(Keys.Account, account);
        }

        public Account GetAccount()
        {
            return HttpContext.Current.Session[Keys.Account] as Account;
        }
    }
}
