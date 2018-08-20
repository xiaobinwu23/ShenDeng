using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using NHibernate.Transform;
using ShenDeng.Framework.App_Start;

namespace ShenDeng.Framework.Handle
{
    [RegisterToContainer]
    public class PassWord_Handle : IPassWord_Handle
    {
        //随机填充的字节长度
        private int random_count = 5;

        public byte[] CreateDbPassword(string password)
        {
            SHA1 sha1 = SHA1.Create();
            //得到原始密码的哈希值。为20位的byte数组
            var hash_spwd = sha1.ComputeHash(Encoding.Unicode.GetBytes(password));
            //得到随机填充的字节数组
            var random_byte = new byte[random_count];
            var rng =new RNGCryptoServiceProvider();
            rng.GetBytes(random_byte);
            //把哈希后的密码和随机填充的随机数组拼接
            var pwd_random_byte = new byte[hash_spwd.Length + random_count];
            hash_spwd.CopyTo(pwd_random_byte, 0);
            random_byte.CopyTo(pwd_random_byte, hash_spwd.Length);
            //哈希拼接后的字节数组
            var hash_pwd_random = sha1.ComputeHash(pwd_random_byte);
            //把随机字节拼接到哈希后的密码和随机字节，得到最终的密码
            var dbpwd = new byte[hash_pwd_random.Length + random_count];
            hash_pwd_random.CopyTo(dbpwd, 0);
            random_byte.CopyTo(dbpwd, hash_pwd_random.Length);
            return dbpwd;
        }

        public bool ComparePassword(string password, byte[] dbpassword)
        {
            SHA1 sha1 = SHA1.Create();
            //哈希密码
            var hash_pwd = sha1.ComputeHash(Encoding.Unicode.GetBytes(password));
            //获取随机字节
            var random_byte = new byte[random_count];
            int No_random = dbpassword.Length - random_count;
            for (int i = 0; i < random_count; i++)
                random_byte[i] = dbpassword[No_random + i];
            //拼接
            var pwd_random = new byte[hash_pwd.Length + random_count];
            hash_pwd.CopyTo(pwd_random, 0);
            random_byte.CopyTo(pwd_random, hash_pwd.Length);
            //哈希拼接后的
            var hash_pwd_random = sha1.ComputeHash(pwd_random);
            //用户的最终密码
            var end_pwd = new byte[hash_pwd_random.Length + random_count];
            hash_pwd_random.CopyTo(end_pwd, 0);
            random_byte.CopyTo(end_pwd, hash_pwd_random.Length);
            //比较
            return Compare(end_pwd, dbpassword);
        }

        public bool Compare(byte[] userPwd, byte[] dbPwd)
        {
            if (userPwd.Length != dbPwd.Length)
                return false;
            for (int i = 0; i < dbPwd.Length; i++)
            {
                if (userPwd[i] != dbPwd[i])
                return false;
            }
            return true;
        }
    }
}
