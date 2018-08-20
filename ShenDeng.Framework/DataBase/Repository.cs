using System;
using System.CodeDom;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using LinqSpecs;
using Machine.Specifications.Model;
using NHibernate;
using ShenDeng.Framework.App_Start;
using ShenDeng.Framework.Base;

namespace ShenDeng.Framework.DataBase
{
    [RegisterToContainer]
    public class Repository : IRepository
    {
        public ISession session { set; get; }

        public Repository()
        {
            session = CreateSessionFactory.GetSession();
        }
        //保存
        public void Save<TEntity>(TEntity entity)
            where TEntity : IEntity
        {
            if (entity.DBID == Guid.Empty)
                entity.SaveTime = DateTime.Now;
            entity.EditTime = DateTime.Now;
            entity.SaveUser = "神灯同学";

            session.SaveOrUpdate(entity);
        }
        //找所有
        public IEnumerable<TEntity> FindAll<TEntity>()
            where TEntity : IEntity
        {
            return session.Query<TEntity>().ToList();
        }
        //根据特定数据源筛选
        private IQueryable<TEntity> GetQuery<TEntity>(Specification<TEntity> spe)
        {
            return session.Query<TEntity>()
                .Where(spe.ToExpression());
        }
        //找一个
        public TEntity FindOne<TEntity>(Specification<TEntity> spe)
            where TEntity : IEntity
        {
            var entitys = GetQuery(spe).ToList();
            if (entitys.Count() != 1)
               throw new Exception("查询结果不存在!");
            return entitys.Single();
        }
        //是否存在
        public bool IsExisted<TEntity>(Specification<TEntity> spe)
            where TEntity : IEntity
        {
            var entity = GetQuery(spe).ToList();
            return entity.Count >= 1;
        }
        //删除
        public void Delete<TEntity>(TEntity entity)
            where TEntity : IEntity
        {
            try
            {
                if (entity.CanDelete)
                {
                    session.Delete(entity);
                    var transaction = session.Transaction;
                    transaction.Commit();
                }
                
            }
            catch (Exception e)
            {
                throw new Exception("该实体不存在");
            }
        }
    }
}
