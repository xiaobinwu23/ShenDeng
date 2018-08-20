using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using FluentNHibernate.Mapping;

namespace ShenDeng.Framework.Base
{
    public class BaseClassMap<T> : ClassMap<T> 
        where T : Entity<T>
    {
        public BaseClassMap()
        {
            Id(x => x.DBID).GeneratedBy.GuidComb();  //GeneratedBy：指定这个DBID的生产者
            Map(x => x.SaveUser);
            Map(x => x.SaveTime);
            Map(x => x.EditTime);
            Map(x => x.CanDelete);
        }
    }
}
