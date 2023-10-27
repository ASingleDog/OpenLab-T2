import { Card, Input, Form, Button } from 'antd'
import cookie from 'react-cookies'
import { rsaEncrypt } from '../utils/coder';

interface FieldType {
  id: number;
  psw: string;
}

interface LoginResponse {
  code: number;
  msg?: string;
  token?: string;
  admin?: boolean;
}

const BaseURL = ''


let setTokenFunc: (s: string) => void

async function handleLogin(value: FieldType) {

  const res = await fetch(BaseURL + '/api/user/login', {
    method: 'POST',
    cache: "no-cache",
    redirect: "follow",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: value.id,
      code: rsaEncrypt(value.psw)
    })
  })

  if (res.status == 200) {
    const data: LoginResponse = await res.json()
    if (data.code == 200) {
      cookie.save('token', data.token!, { path: '/', maxAge: 24 * 60 * 60 * 1000 })
      if (data.admin!) 
        cookie.save('admin', 1, { path: '/', maxAge: 24 * 60 * 60 * 1000 })
      else 
        cookie.save('admin', 0, { path: '/', maxAge: 24 * 60 * 60 * 1000 })
      
      cookie.save('uid', value.id, { path: '/', maxAge: 24 * 60 * 60 * 1000 })
      setTokenFunc(data.token!)
    }
    else {
      alert(data.msg)
    }
  }
}


const Login = ({ setToken, setIsLoginPage }) => {
  setTokenFunc = setToken

  return (
    <Card title="登录" style={{ width: 500 }}>
      <Form
        name="basic"
        labelCol={{ span: 7 }}
        wrapperCol={{ span: 15 }}
        style={{ maxWidth: 400 }}
        size='large'
        onFinish={handleLogin}
      >
        <Form.Item<FieldType>
          label="学号"
          name="id"
          initialValue={123456}
          rules={[{ required: true, message: '请输入学号!', pattern: /^[0-9]{6,}$/ }]}
        >
          <Input />
        </Form.Item>

        <Form.Item<FieldType>
          label="密码"
          name="psw"
          initialValue='admin'
          rules={[{ required: true, message: '请输入不少于5位的密码!', pattern: /^.{5,}$/ }]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item wrapperCol={{ offset: 8, span: 16 }} style={{ marginTop: 30 }}>
          <Button type="primary" htmlType="submit">
            登录
          </Button>

          <Button type="dashed" style={{ marginLeft: '10%' }} onClick={() => setIsLoginPage(false)}>
            注册
          </Button>
        </Form.Item>



      </Form>
    </Card>
  )
}

export default Login