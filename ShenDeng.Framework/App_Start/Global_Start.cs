using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ShenDeng.Framework.Application;
using ShenDeng.Framework.DataBase;
using ShenDeng.Framework.Domain;

namespace ShenDeng.Framework.App_Start
{
    public static class Global_Start
    {
        private static IAccountService accountService = UnityIoC.Get<IAccountService>();
        private static IRepository repository = UnityIoC.Get<IRepository>();
        public static void CreateAccount()
        {
            if (!repository.IsExisted(new Account.By(AccountIdentifier.of("admin"))))
               accountService.CreateAccount("admin")
                   .SetPassWord("1")
                   .SetRole(Role.Admin)
                   .SetCanDelete(false)
                   .Commit();
        }
    }
}
