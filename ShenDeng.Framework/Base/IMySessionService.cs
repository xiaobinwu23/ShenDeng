using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ShenDeng.Framework.Domain;

namespace ShenDeng.Framework.Base
{
    public interface IMySessionService
    {
        void Login(string username, bool rememberMe);
        void SignOut();
        void SaveAccount(Account account);
        Account GetAccount();
    }
}
