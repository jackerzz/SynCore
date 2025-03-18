#!/bin/bash
# conda activate ray
#!/bin/bash

# 1. 生成命令（自动去除多余空格）
apps=$(find . -type f -name '*_service.py' -exec basename {} .py \; | sed 's/$/:app/' | tr '\n' ' ')
cmd=$(echo "serve build $apps -o script/config.yaml" | sed 's/  */ /g')

# 2. 打印将要执行的命令（用于确认）
echo "即将执行命令："
echo "$cmd"

# 3. 等待用户确认
read -p "确认执行命令？(y/n) " -n 1 -r
echo

# 4. 执行命令
if [[ $REPLY =~ ^[Yy]$ ]]; then
    eval $cmd
else
    echo "已取消执行"
fi


# ray start --head

# serve deploy script/config.yaml