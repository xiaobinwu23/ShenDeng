using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ShenDeng.Framework.Handle
{
    public interface IPassWord_Handle
    {
        byte[] CreateDbPassword(string password);
        bool ComparePassword(string password, byte[] dbpassword);
    }
}
