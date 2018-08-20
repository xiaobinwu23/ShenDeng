using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Text;
using System.Threading.Tasks;
using FluentNHibernate.Data;
using ShenDeng.Framework.Base;

namespace ShenDeng.Framework.Domain
{
   public partial class Account : Entity<Account>
    {
        public Account(AccountIdentifier id)
        {
            this.Id = id;
            this.roles = 0;
        }

        public Account()
        {
            
        }
        public virtual AccountIdentifier Id { set; get; }
        public virtual byte[] PassWord { set; get; }   //强随机数填充，哈希加密，25位比特数组
        private int roles;  //采用二进制权限管理
        public virtual int Roles => roles; //只读
        //加权限
        public virtual void AddRole(int role)
        {
            if ((roles & role) == role)
                throw new Exception("用户已有此权限！");
            roles = roles | role;
        }
        //减权限
        public virtual void Remove(int role)
        {
            if ((roles & role) != role)
                throw new Exception("用户没有此权限！");
            roles = roles & (~role);
        }
    }
}
