using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ShenDeng.Framework.Domain
{
    public struct AccountIdentifier
    {
        public string UserName { get; }

        public AccountIdentifier(string username)
        {
            this.UserName = username;
        }

        public static AccountIdentifier of(string username)
        {
            return new AccountIdentifier(username);
        }

        public override string ToString()
        {
            return string.Format("Account/{0}", UserName);
        }

        public static implicit operator string(AccountIdentifier identifier)
        {
            return identifier.ToString();
        }

        public static implicit operator AccountIdentifier(string identifier)
        {
            var sub = identifier.Split(new[] {'/'}, 2);
            return of(sub[1]);
        }
    }
}
