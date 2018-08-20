using System.Web.Mvc;
using ShenDeng.Framework.Application;
using ShenDeng.Framework.Base;
using ShenDeng.Framework.Domain;
using ShenDeng.Framework.Handle;


namespace ShenDeng.Web.Areas.Admin.Controllers
{
    [FilterAuthority(Role.Admin)]
    public class AdminController : Controller
    {
        public readonly IAccountService accountService;
        public AdminController(IAccountService accountService)
        {
            this.accountService = accountService;
        }
        public ActionResult Index()
        {
            return View();
        }

        public ActionResult ManageAccount()
        {
            var accounts = accountService.GetAllAccount();
            return View(accounts);
        }
        //删除账户
        public ActionResult Delete_Account(string id)
        {
            accountService.Delete(AccountIdentifier.of(id));
            return RedirectToAction("ManageAccount");
        }
    }
}