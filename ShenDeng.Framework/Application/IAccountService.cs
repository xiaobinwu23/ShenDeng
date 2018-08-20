using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ShenDeng.Framework.Domain;

namespace ShenDeng.Framework.Application
{
   public interface IAccountService
   {
       IAccountCommand CreateAccount(string username);
       IEnumerable<Account> GetAllAccount();
       Account GetOneAccount(AccountIdentifier id);
       bool Verify(string username, string password);
       void Delete(AccountIdentifier id);
       IAccountCommand EditAccount(AccountIdentifier id);
   }
}
