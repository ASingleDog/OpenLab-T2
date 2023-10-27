import type { ProColumns } from '@ant-design/pro-components';
import {
  EditableProTable,
} from '@ant-design/pro-components';
import { Button, Card } from 'antd';
import React, { useEffect, useState } from 'react';
import cookie from 'react-cookies'
import './RankingTable.css'

type DataSourceType = {
  id: number;
  rank: number;
  name: string;
  score1: number;
  score2: number;
  score3: number;
  score4: number;
  total: number;
};

const defaultData: DataSourceType[] = [
];

function nameCellRender(text: any) {
  const data: DataSourceType = text!
  if (data.id == cookie.load('uid')) {
    return (
      <div style={{ color: '#4096ff', fontWeight: 600 }}>{data.name} (我)</div>
    )
  }
  else {
    return (
      <div>{data.name}</div>
    )
  }

}

function scoreCellRender(text: any) {
  return (
    <div style={
      text.props.text < 10
        ? { color: 'red' }
        : { color: 'green' }
    }>{text.props.text}
    </div>
  )
}

let setDataSourceFunc: React.Dispatch<readonly DataSourceType[]>;
let setLoadingFunc: React.Dispatch<boolean>;
let setTokenFunc: React.Dispatch<string>;

// !!!!!!!!!!!!!!!!!!!!!!!!!
const BaseURL = '' 

async function fetch_data() {
  // setLoading(true)
  const res = await fetch(BaseURL + '/api/data/get?token=' + cookie.load('token'))
  if (res.status == 200) {
    const data: DataSourceType[] = await res.json()
    if(data){
      setDataSourceFunc(data)
      setLoadingFunc(false)
    }
    else{
      alert('未登录或无法使用cookie(例如本地文件)')
    }
    
  }
  else {
    alert('无效token')
    cookie.remove('token')
    setTokenFunc(null)
  }
}

interface ResponseData {
  code: number;
  msg: string;
}

async function update_data(data: DataSourceType) {
  const res = await fetch(BaseURL + '/api/data/update?token=' + cookie.load('token'), {
    method: "PUT",
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  if (res.status == 200) {
    const res_data: ResponseData = await res.json()
    if (res_data.code == 200) {
      setLoadingFunc(true)
      fetch_data()
    }
    else {
      alert(res_data.msg)
    }
  }
  else {
    alert('修改失败，无效数据或token')
  }
}

async function delete_data(data: DataSourceType) {
  const res = await fetch(BaseURL + `/api/data/delete?id=${data.id}&token=${cookie.load('token')}`, {
    method: "DELETE",
  })
  if (res.status == 200) {
    const res_data: ResponseData = await res.json()
    if (res_data.code == 200) {
      setLoadingFunc(true)
      fetch_data()
    }
    else {
      alert(res_data.msg)
    }
  }
  else {
    alert('删除失败，无效数据或token')
  }
}


export default function RankTable({ setToken }: { setToken: React.Dispatch<string> }) {
  const [loading, setLoading] = useState(true);
  const [editableKeys, setEditableRowKeys] = useState<React.Key[]>([]);
  const [dataSource, setDataSource] = useState<readonly DataSourceType[]>(defaultData);
  setDataSourceFunc = setDataSource
  setLoadingFunc = setLoading
  setTokenFunc = setToken

  const columns: ProColumns<DataSourceType>[] = [
    {
      title: '排名',
      dataIndex: 'rank',
      editable: false,
    },
    {
      title: '姓名',
      // dataIndex: 'name',
      editable: false,
      render: nameCellRender,
      width: '20%',
    },
    {
      title: 'T1',
      dataIndex: 'score1',
      valueType: 'digit',
      render: scoreCellRender
    },
    {
      title: 'T2',
      dataIndex: 'score2',
      valueType: 'digit',
      render: scoreCellRender
    },
    {
      title: 'T3',
      dataIndex: 'score3',
      valueType: 'digit',
      render: scoreCellRender
    },
    {
      title: 'T4',
      dataIndex: 'score4',
      valueType: 'digit',
      render: scoreCellRender

    },
    {
      title: '总分',
      dataIndex: 'total',
      // render: totalScoreCellRender,
      valueType: 'digit',
      // valueType: 'date',
      editable: false
    },
    {
      title: '操作',
      valueType: 'option',
      render: (text, record, _, action) => [
        <Button
          key="editable"
          onClick={() => {
            action?.startEditable?.(record.id);
          }}
          type='link'
          disabled={cookie.load('admin') == 0}
        >
          编辑
        </Button>,
      ],
    },
  ];

  useEffect(() => { if (dataSource && dataSource.length <= 0) fetch_data() })

  return (
    <>
      <Card>
        <EditableProTable<DataSourceType>
          rowKey="id"
          headerTitle={(cookie.load('admin') == 1) ? "用户权限：管理员" : "用户权限：普通用户"}
          maxLength={6}
          scroll={{
            x: 960,
          }}

          loading={loading}

          columns={columns}

          value={dataSource}

          onChange={setDataSource}

          recordCreatorProps={{
            record: null,
            style: {
              display: 'none',
            }
          }}

          editable={{
            type: 'single',
            editableKeys,
            onSave: async (rowKey, data) => {
              // console.log(rowKey, data, row);
              await update_data(data)
            },
            onChange: setEditableRowKeys,
            onDelete: async (key, row) => {
              await delete_data(row)
            },
            deletePopconfirmMessage: '删除此项并注销该用户?'
          }}


        />
        <div className='BtnBox'>
          <Button onClick={() => { setLoading(true); fetch_data() }} type='primary'>
            重新获取
          </Button>

          <Button onClick={() => { cookie.remove('token'); setToken(null); }} style={{ marginLeft: 10 }}>
            退出登录
          </Button>
        </div>
      </Card>


    </>
  );
}
