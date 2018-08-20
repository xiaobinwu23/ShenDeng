using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ShenDeng.Framework.Base
{
   public interface IEntity
    {
        Guid DBID { get; }
        DateTime SaveTime { set; get; }
        DateTime EditTime { set; get; }
        string SaveUser { set; get; }
        bool CanDelete { set; get; }
    }
}
