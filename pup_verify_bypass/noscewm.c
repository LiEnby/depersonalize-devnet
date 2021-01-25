// lol just remove scewm and now they cant track ya

#include <stdio.h>
#include <stdarg.h>
#include <vitasdk.h>
#include <taihen.h>

static int hook = -1;
static tai_hook_ref_t ref_hook;

static int sceSblUsVerifyPup_patched(char* path) {
	int ret = TAI_CONTINUE(int, ref_hook,path);
	if(ret == 0x800F0216)
		return 0;
	return ret;
}

void _start() __attribute__ ((weak, alias ("module_start")));
int module_start(SceSize argc, const void *args)
{
	hook = taiHookFunctionExportForKernel(KERNEL_PID,
		&ref_hook, 
		"SceSblUpdateMgr",
		0x31406C49,
		0x6F5EDBF4, 
		sceSblUsVerifyPup_patched);
	return SCE_KERNEL_START_SUCCESS;
}

int module_stop(SceSize argc, const void *args)
{
	if (hook >= 0) taiHookReleaseForKernel(hook, ref_hook);   
	return SCE_KERNEL_STOP_SUCCESS;
}
