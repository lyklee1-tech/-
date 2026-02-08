"""
스케줄러 모듈
"""
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from loguru import logger
import yaml
import sys
import os

# 메인 자동화 클래스 임포트
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import EconomicShortsAutomation


class AutomationScheduler:
    """고급 스케줄링 시스템"""
    
    def __init__(self, config_path='config/config.yaml'):
        self.config_path = config_path
        
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            self.scheduler_config = config['scheduler']
        
        # 스케줄러 초기화
        self.scheduler = BlockingScheduler()
        self.automation = EconomicShortsAutomation(config_path)
        
        logger.info("스케줄러 초기화 완료")
    
    def job_wrapper(self):
        """작업 실행 래퍼 (에러 핸들링 포함)"""
        retry_config = self.scheduler_config['retry']
        max_attempts = retry_config['max_attempts']
        delay = retry_config['delay']
        
        for attempt in range(1, max_attempts + 1):
            try:
                logger.info(f"\n{'=' * 60}")
                logger.info(f"작업 시작 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                logger.info(f"시도: {attempt}/{max_attempts}")
                logger.info(f"{'=' * 60}\n")
                
                # 메인 작업 실행
                self.automation.run_single()
                
                logger.info(f"\n✅ 작업 완료 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                return  # 성공하면 종료
                
            except Exception as e:
                logger.error(f"작업 실패 (시도 {attempt}/{max_attempts}): {e}")
                
                if attempt < max_attempts:
                    logger.info(f"{delay}초 후 재시도...")
                    import time
                    time.sleep(delay)
                else:
                    logger.error("최대 재시도 횟수 초과. 작업 실패.")
    
    def setup_schedule(self):
        """스케줄 설정"""
        mode = self.scheduler_config['mode']
        
        if mode == 'hourly':
            # 시간별 실행
            interval = self.scheduler_config['hourly']['interval']
            self.scheduler.add_job(
                self.job_wrapper,
                'interval',
                hours=interval,
                id='hourly_job',
                replace_existing=True
            )
            logger.info(f"스케줄 설정: {interval}시간마다 실행")
        
        elif mode == 'daily':
            # 일별 특정 시간 실행
            times = self.scheduler_config['daily']['times']
            for i, time_str in enumerate(times):
                hour, minute = map(int, time_str.split(':'))
                self.scheduler.add_job(
                    self.job_wrapper,
                    'cron',
                    hour=hour,
                    minute=minute,
                    id=f'daily_job_{i}',
                    replace_existing=True
                )
                logger.info(f"스케줄 설정: 매일 {time_str}에 실행")
        
        elif mode == 'custom':
            # 커스텀 cron 표현식
            cron_expr = self.scheduler_config['custom']['cron']
            self.scheduler.add_job(
                self.job_wrapper,
                CronTrigger.from_crontab(cron_expr),
                id='custom_job',
                replace_existing=True
            )
            logger.info(f"스케줄 설정: {cron_expr}")
        
        else:
            logger.error(f"알 수 없는 스케줄 모드: {mode}")
            return False
        
        return True
    
    def start(self):
        """스케줄러 시작"""
        if not self.scheduler_config['enabled']:
            logger.warning("스케줄러가 비활성화되어 있습니다")
            return
        
        if not self.setup_schedule():
            logger.error("스케줄 설정 실패")
            return
        
        logger.info("\n" + "=" * 60)
        logger.info("🚀 스케줄러 시작")
        logger.info("=" * 60)
        logger.info(f"모드: {self.scheduler_config['mode']}")
        logger.info("등록된 작업:")
        for job in self.scheduler.get_jobs():
            logger.info(f"  - {job.id}: {job.trigger}")
        logger.info("\nCtrl+C를 눌러 종료")
        logger.info("=" * 60 + "\n")
        
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("\n스케줄러 종료")


if __name__ == "__main__":
    logger.add("logs/scheduler.log", rotation="1 day")
    
    scheduler = AutomationScheduler()
    scheduler.start()
