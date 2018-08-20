using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ShenDeng.Framework.Base
{
    public class Entity<TEntity> : IEntity where TEntity:IEntity
    {
       public Entity()
       {
           CanDelete = true;
       }

        public virtual Guid DBID { protected set; get; }
        public virtual DateTime SaveTime { set; get; }
        public virtual DateTime EditTime { set; get; }
        public virtual string SaveUser { set; get; }
        public virtual bool CanDelete { set ; get; }
    }
}