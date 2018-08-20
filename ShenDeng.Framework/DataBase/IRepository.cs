using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using LinqSpecs;
using Machine.Specifications.Model;
using NHibernate;
using NHibernate.Transform;
using ShenDeng.Framework.Base;

namespace ShenDeng.Framework.DataBase
{
    public interface IRepository
    {
        ISession session { set; get; }
        void Save<TEntity>(TEntity entity) where TEntity : IEntity;
        IEnumerable<TEntity> FindAll<TEntity>() where TEntity : IEntity;
        TEntity FindOne<TEntity>(Specification<TEntity> spe) where TEntity : IEntity;
        bool IsExisted<TEntity>(Specification<TEntity> spe) where TEntity : IEntity;
        void Delete<TEntity>(TEntity entity) where TEntity : IEntity;
    }
}
