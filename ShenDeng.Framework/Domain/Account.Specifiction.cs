using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
using System.Text;
using System.Threading.Tasks;
using LinqSpecs;

namespace ShenDeng.Framework.Domain
{
    public partial class Account
    {
        public class By : Specification<Account>
        {
            public readonly AccountIdentifier _id;

            public By(AccountIdentifier id)
            {
                this._id = id;
            }
            public override Expression<Func<Account, bool>> ToExpression()
            {
                return x => x.Id.UserName == _id.UserName;
            }
        }
    }
}
