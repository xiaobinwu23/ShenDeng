using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ShenDeng.Framework.DataBase;
using ShenDeng.Framework.Domain;
using ShenDeng.Framework.Handle;

namespace ShenDeng.Framework.Application.Imp
{
    public class AccountCommand : IAccountCommand
    {
        public  Account account;
        public IRepository repository;
        public PassWord_Handle passwordService;

        public AccountCommand(Account account,
            IRepository repository,
            PassWord_Handle passwordService)
        {
            this.repository = repository;
            this.account = account;
            this.passwordService = passwordService;
        }
        //设置密码
        public IAccountCommand SetPassWord(string password)
        {
            account.PassWord = passwordService.CreateDbPassword(password);
            
            return this;
        }
        //添加角色
        public IAccountCommand SetRole(Role role)
        {
            account.AddRole((int)role);
            return this;
        }
        //提交事务
        public void Commit()
        {
            var trancation = repository.session.Transaction;
            trancation.Commit();  //提交本次数据库操作。
        }
        //是否能被删除
        public IAccountCommand SetCanDelete(bool candelete)
        {
            account.CanDelete = candelete;
            return this;
        }
    }
}

