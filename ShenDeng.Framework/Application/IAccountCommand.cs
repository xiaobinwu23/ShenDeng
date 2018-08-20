using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ShenDeng.Framework.Domain;

namespace ShenDeng.Framework.Application
{
    public interface IAccountCommand
    {
        IAccountCommand SetPassWord(string password);
        IAccountCommand SetRole(Role role);
        IAccountCommand SetCanDelete(bool candelete);
        void Commit();
    }
}
