using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using FluentNHibernate.Mapping;
using ShenDeng.Framework.Base;
using ShenDeng.Framework.Domain;

namespace ShenDeng.Framework.Map
{
    public class AccountMap : BaseClassMap<Account>
    {
        public AccountMap()
        {
            Component(x => x.Id, y => y.Map(m => m.UserName).Unique());
            Map(x => x.PassWord).CustomType<byte[]>().Length(25);
            Map(x => x.Roles);
        }
    }
}
