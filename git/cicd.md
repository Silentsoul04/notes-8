```
  except:
    variables:
    - $CI_COMMIT_MESSAGE =~ /skip-docker-compose-test/
```
commit message 填写跳过compose