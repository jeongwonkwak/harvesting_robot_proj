# Git / GitHub 명령어 정리

---

## 초기 설정

```bash
git config --global user.name "이름"
git config --global user.email "이메일"
git config --global core.editor "vim"      # 기본 에디터 설정
git config --list                           # 설정 확인
```

---

## 저장소 생성 / 복제

```bash
git init                                    # 현재 폴더를 git 저장소로 초기화
git clone <URL>                             # 원격 저장소 복제
git clone <URL> <폴더명>                    # 특정 폴더명으로 복제
git clone -b <브랜치명> <URL>              # 특정 브랜치만 복제
```

---

## 상태 확인

```bash
git status                                  # 현재 작업 상태 확인
git log                                     # 커밋 히스토리
git log --oneline                           # 한 줄로 간략하게
git log --oneline --graph --all             # 브랜치 그래프 포함
git diff                                    # 변경사항 확인 (unstaged)
git diff --staged                           # 스테이징된 변경사항 확인
```

---

## 스테이징 & 커밋

```bash
git add <파일명>                            # 특정 파일 스테이징
git add .                                   # 전체 변경사항 스테이징
git add -p                                  # 변경사항을 부분적으로 스테이징

git commit -m "커밋 메시지"                 # 커밋
git commit -am "커밋 메시지"               # add + commit 동시에 (tracked 파일만)

git restore <파일명>                        # 작업 디렉토리 변경사항 취소
git restore --staged <파일명>               # 스테이징 취소
```

---

## 브랜치

```bash
git branch                                  # 로컬 브랜치 목록
git branch -r                               # 원격 브랜치 목록
git branch -a                               # 전체 브랜치 목록

git branch <브랜치명>                       # 브랜치 생성
git checkout <브랜치명>                     # 브랜치 이동
git checkout -b <브랜치명>                  # 브랜치 생성 + 이동
git checkout -b <브랜치명> origin/<브랜치명> # 원격 브랜치를 로컬에 생성 + 이동

git branch -d <브랜치명>                    # 브랜치 삭제 (병합된 경우)
git branch -D <브랜치명>                    # 브랜치 강제 삭제
git branch -m <기존명> <새이름>             # 브랜치 이름 변경
```

---

## 원격 저장소 (Remote)

```bash
git remote -v                               # 원격 저장소 목록 확인
git remote add origin <URL>                 # 원격 저장소 연결
git remote remove origin                    # 원격 저장소 연결 해제
git remote set-url origin <URL>             # 원격 저장소 URL 변경
```

---

## fetch / pull / push

```bash
# fetch: 원격 변경사항을 가져오되 병합하지 않음
git fetch origin                            # 전체 fetch
git fetch origin <브랜치명>                 # 특정 브랜치 fetch

# pull: fetch + merge
git pull origin <브랜치명>                  # 원격 브랜치 pull (merge)
git pull origin <브랜치명> --no-rebase      # merge 방식
git pull origin <브랜치명> --rebase         # rebase 방식

# push: 로컬 커밋을 원격에 업로드
git push origin <브랜치명>                  # 원격에 push
git push -u origin <브랜치명>               # 업스트림 설정하며 push (이후 git push만으로 가능)
git push origin --delete <브랜치명>         # 원격 브랜치 삭제
git push --force origin <브랜치명>          # 강제 push (주의!)
```

---

## Merge / Rebase

```bash
git merge <브랜치명>                        # 현재 브랜치에 병합
git merge --no-ff <브랜치명>               # merge 커밋 강제 생성
git merge --abort                           # 충돌 시 merge 취소

git rebase <브랜치명>                       # rebase
git rebase --abort                          # rebase 취소
git rebase --continue                       # 충돌 해결 후 rebase 계속
```

---

## 되돌리기

```bash
# reset: 커밋 취소
git reset --soft HEAD~1                     # 커밋만 취소 (변경사항 staged 유지)
git reset --mixed HEAD~1                    # 커밋 + 스테이징 취소 (변경사항 유지)
git reset --hard HEAD~1                     # 커밋 + 변경사항 모두 취소

# 원격 브랜치와 동일하게 맞추기
git reset --hard origin/<브랜치명>

# revert: 특정 커밋을 되돌리는 새 커밋 생성 (히스토리 보존)
git revert <커밋해시>
```

---

## Stash (임시 저장)

```bash
git stash                                   # 현재 변경사항 임시 저장
git stash save "메모"                       # 메모와 함께 저장
git stash list                              # stash 목록
git stash pop                               # 가장 최근 stash 적용 + 삭제
git stash apply stash@{0}                   # 특정 stash 적용 (삭제 안 함)
git stash drop stash@{0}                    # 특정 stash 삭제
git stash clear                             # 전체 stash 삭제
```

---

## Tag

```bash
git tag                                     # 태그 목록
git tag <태그명>                            # 태그 생성 (lightweight)
git tag -a <태그명> -m "메시지"             # annotated 태그 생성
git push origin <태그명>                    # 태그 원격에 push
git push origin --tags                      # 전체 태그 push
git tag -d <태그명>                         # 태그 삭제
```

---

## 자주 쓰는 상황별 정리

### 원격 브랜치를 로컬에 받아올 때
```bash
git fetch origin <브랜치명>
git checkout -b <브랜치명> origin/<브랜치명>
```

### 로컬을 원격과 완전히 동일하게 맞출 때 (로컬 변경사항 포기)
```bash
git fetch origin <브랜치명>
git reset --hard origin/<브랜치명>
```

### 브랜치 갈라진 경우 (diverged) 해결
```bash
git pull origin <브랜치명> --no-rebase     # merge로 합치기
git pull origin <브랜치명> --rebase        # rebase로 합치기
git reset --hard origin/<브랜치명>         # 원격으로 덮어쓰기
```

### 실수로 커밋한 파일 제거
```bash
git rm --cached <파일명>                   # 추적에서 제거 (파일은 유지)
git commit -m "파일 추적 제거"
```

---

> **주의사항**
> - `reset --hard`, `push --force`는 작업 내용이 사라질 수 있으니 신중하게 사용
> - 팀 작업 시 공유 브랜치에 `force push`는 금지
