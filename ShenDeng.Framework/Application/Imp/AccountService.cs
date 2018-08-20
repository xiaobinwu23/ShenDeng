using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using NHibernate;
using ShenDeng.Framework.Base;
using ShenDeng.Framework.DataBase;
using ShenDeng.Framework.Domain;
using ShenDeng.Framework.Handle;
using System.Web.Mvc;
using ShenDeng.Framework.App_Start;

namespace ShenDeng.Framework.Application.Imp
{
    [RegisterToContainer]
    public class AccountService : IAccountService
    {
        public readonly IRepository repository;
        public PassWord_Handle passwordService;
        public AccountService(IRepository repository,
            PassWord_Handle passwordService)
        {
            this.repository = repository;
            this.passwordService = passwordService;
        }
        //增
        public IAccountCommand CreateAccount(string username)
        {
            if (repository.IsExisted(new Account.By(AccountIdentifier.of(username))))
                 throw new Exception("用户名已存在！");
            var account = new Account(AccountIdentifier.of(username));    
            repository.Save(account);
            return new AccountCommand(account, repository, passwordService);
        }
        //删
        public void Delete(AccountIdentifier id)
        {
            var account = repository.FindOne(new Account.By(id));
            repository.Delete(account);

        }
        //找s
        public IEnumerable<Account> GetAllAccount()
        {
            return repository.FindAll<Account>();
        }
        //找
        public Account GetOneAccount(AccountIdentifier id)
        {
            return repository.FindOne(new Account.By(id));
        }
        //改
        public IAccountCommand EditAccount(AccountIdentifier id)
        {
            var account = GetOneAccount(id);
            repository.Save(account);
            return new AccountCommand(account, repository, passwordService);
        }
        //证
        public bool Verify(string username, string password)
        {
            var account = GetOneAccount(AccountIdentifier.of(username));
            return passwordService.ComparePassword(password, account.PassWord);
        }
    }
}
